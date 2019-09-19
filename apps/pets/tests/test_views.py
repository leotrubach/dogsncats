from django.urls import reverse
from apps.pets import models
from .factories import CatFactory, DogFactory, OwnerFactory

DUMMY_NAME = "foobar"
DUMMY_DATE = "2019-09-19"

MODEL_CLASSES = (("dog", models.Dog), ("cat", models.Cat))
MODEL_FACTORIES = (("dog", DogFactory), ("cat", CatFactory))


def test_owner_sees_all_of_pets(ownerclient):
    CatFactory()
    DogFactory()
    for model, klass in MODEL_CLASSES:
        resp = ownerclient.get(reverse(f"api:{model}-list"))
        assert resp.status_code == 200
        ids = [o["id"] for o in resp.data]
        db_ids = [o.id for o in klass.objects.all()]
        assert set(ids) == set(db_ids)


def test_owner_can_edit_their_pets(ownerclient):
    for model, klass in MODEL_CLASSES:
        my_pet = klass.objects.first()
        resp = ownerclient.patch(
            reverse(f"api:{model}-detail", args=(my_pet.pk,)), data={"name": DUMMY_NAME}
        )
        assert resp.status_code == 200
        my_pet.refresh_from_db()
        assert my_pet.name == "foobar"


def test_owner_cant_edit_their_pets_owner(ownerclient):
    owner = models.Owner.objects.first()
    other_owner = OwnerFactory()
    for model, klass in MODEL_CLASSES:
        my_pet = klass.objects.first()
        resp = ownerclient.patch(
            reverse(f"api:{model}-detail", args=(my_pet.pk,)),
            data={"owner": other_owner.pk},
        )
        assert resp.status_code == 403
        my_pet.refresh_from_db()
        assert my_pet.owner == owner


def test_owner_can_delete_their_pets(ownerclient):
    cats_before = models.Cat.objects.count()
    dogs_before = models.Dog.objects.count()
    for model, klass in MODEL_CLASSES:
        my_pet = klass.objects.first()
        resp = ownerclient.delete(reverse(f"api:{model}-detail", args=(my_pet.pk,)))
        assert resp.status_code == 204
    cats_after = models.Cat.objects.count()
    dogs_after = models.Dog.objects.count()
    assert cats_after == cats_before - 1
    assert dogs_after == dogs_before - 1


def test_owner_can_create_their_pets(ownerclient):
    cats_before = models.Cat.objects.count()
    dogs_before = models.Dog.objects.count()
    owner = models.Owner.objects.first()
    for model, _ in MODEL_CLASSES:
        resp = ownerclient.post(
            reverse(f"api:{model}-list"),
            data={"name": DUMMY_NAME, "birthday": DUMMY_DATE, "owner": owner.pk},
        )
        assert resp.status_code == 201
    cats_after = models.Cat.objects.count()
    dogs_after = models.Dog.objects.count()
    assert cats_after == cats_before + 1
    assert dogs_after == dogs_before + 1


def test_owner_cant_create_others_pets(ownerclient):
    cats_before = models.Cat.objects.count()
    dogs_before = models.Dog.objects.count()
    other_owner = OwnerFactory()
    for model, _ in MODEL_CLASSES:
        resp = ownerclient.post(
            reverse(f"api:{model}-list"),
            data={"name": DUMMY_NAME, "birthday": DUMMY_DATE, "owner": other_owner.pk},
        )
        assert resp.status_code == 403
    cats_after = models.Cat.objects.count()
    dogs_after = models.Dog.objects.count()
    assert cats_after == cats_before
    assert dogs_after == dogs_before


def test_owner_cant_edit_other_pets(ownerclient):
    for model, klass in MODEL_FACTORIES:
        other_pet = klass()
        resp = ownerclient.patch(
            reverse(f"api:{model}-detail", args=(other_pet.pk,)),
            data={"name": DUMMY_NAME},
        )
        assert resp.status_code == 403
        other_pet.refresh_from_db()
        assert other_pet.name != DUMMY_NAME


def test_owner_can_edit_their_info(ownerclient):
    owner = models.Owner.objects.first()
    resp = ownerclient.patch(
        reverse("api:owner-detail", args=(owner.pk,)), data={"full_name": DUMMY_NAME}
    )
    assert resp.status_code == 200
    owner.refresh_from_db()
    assert owner.full_name == DUMMY_NAME


def test_owner_cant_delete_themselves(ownerclient):
    owner = models.Owner.objects.first()
    resp = ownerclient.delete(reverse("api:owner-detail", args=(owner.pk,)))
    assert resp.status_code == 403


def test_owner_cant_edit_other_owner(ownerclient):
    owner = OwnerFactory()
    resp = ownerclient.patch(
        reverse("api:owner-detail", args=(owner.pk,)), data={"full_name": DUMMY_NAME}
    )
    assert resp.status_code == 403
    owner.refresh_from_db()
    assert owner.full_name != DUMMY_NAME


def test_owner_cant_add_owner(ownerclient):
    resp = ownerclient.post(reverse("api:owner-list"), data={"full_name": DUMMY_NAME})
    assert resp.status_code == 403
    assert models.Owner.objects.count() == 1
