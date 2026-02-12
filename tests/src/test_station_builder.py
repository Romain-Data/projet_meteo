import pytest

from projet.src.entities.station_builder import StationBuilder
from projet.src.entities.station import Station
from projet.src.entities.weather_report import WeatherReport


@pytest.fixture
def builder():
    return StationBuilder()

@pytest.fixture
def mock_weather_report(mocker):
    return mocker.Mock(spec=WeatherReport)


def test_station_builder_initialization(builder, mock_weather_report):
    builder.set_id("1")
    builder.set_nom("Toulouse")
    builder.set_latitude(1.123)
    builder.set_longitude(3.123)
    builder.reports = [mock_weather_report]

    assert builder.id == "1"
    assert builder.nom == "Toulouse"
    assert builder.latitude == 1.123
    assert builder.longitude == 3.123
    assert builder.reports == [mock_weather_report]
    assert builder.reports[0] == mock_weather_report
    assert len(builder.reports) == 1


def test_return_station_type(builder):
    result = builder.build()

    assert isinstance(result, Station)


def test_set_nom_return_self(builder):
    result = builder.set_nom("Toulouse")
    assert result is builder


def test_set_id_return_self(builder):
    result = builder.set_id("1")
    assert result is builder


def test_set_latitude_return_self(builder):
    result = builder.set_latitude(1.123)
    assert result is builder


def test_set_longitude_return_self(builder):
    result = builder.set_longitude(3.123)
    assert result is builder


def test_set_reports_return_self(builder, mock_weather_report):
    result = builder.set_reports([mock_weather_report])
    assert result is builder


@pytest.mark.parametrize(
    "method, bad_value",
    [
        ("set_id", []),  # invalid ID (list) - int is valid now
        ("set_nom", 123),  # invalid name (int)
        ("set_latitude", "NORD"),  # invalid latitude (str)
        ("set_longitude", "EST"),  # invalid longitude (str)
        ("set_reports", ("A", 2))  # invalid reports (tuple)
    ]
)
def test_builder_type_errors(builder, method, bad_value):
    with pytest.raises(TypeError):
        getattr(builder, method)(bad_value)


def test_chaining_build(builder, mock_weather_report):
    result = builder.set_id(
        "1"
    ).set_nom("A").set_latitude(1.2).set_longitude(12).set_reports([mock_weather_report])
    assert result is builder


def test_set_nom_empty_raises_value_error(builder):
    """Vérifie que set_nom lève une ValueError si le nom est vide"""
    with pytest.raises(ValueError):
        builder.set_nom("")


def test_set_id_accepts_int(builder):
    """Vérifie que set_id accepte un entier"""
    builder.set_id(123)
    assert builder.id == 123


def test_set_id_empty_raises_value_error(builder):
    """Vérifie que set_id lève une ValueError si l'ID est vide"""
    with pytest.raises(ValueError):
        builder.set_id("")
    with pytest.raises(ValueError):
        builder.set_id(0) # 0 est falsy en Python, donc 'if not station_id' sera True