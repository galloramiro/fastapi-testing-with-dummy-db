from src.repositories.crop import CropRepository
from src.schemas import CropRequest, CropResponse


def test_crop_repository_save(setup_database, testing_session):
    crop = CropRequest(name="Test Crop", type="Test type")

    with testing_session.get_session() as session:
        repository = CropRepository(session=session)
        saved_crop = repository.save(crop=crop)
        saved_crop = CropResponse.from_orm(saved_crop)

    assert saved_crop.name == crop.name
    assert saved_crop.type == crop.type


def test_crop_repository_get_all(setup_database, testing_session):
    crop = CropRequest(name="Test Crop", type="Test type")

    with testing_session.get_session() as session:
        repository = CropRepository(session=session)
        repository.save(crop=crop)

        quantity_of_crops = len(repository.get_all())

    assert quantity_of_crops == 1
