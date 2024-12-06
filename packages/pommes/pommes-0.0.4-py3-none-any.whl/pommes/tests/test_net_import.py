import numpy as np
import pytest
import xarray as xr
from numpy.testing import assert_array_equal as assert_equal

from pommes.model.build_model import build_model


@pytest.fixture()
def parameter_net_import(parameters_dispatch_invest, net_import):
    p = xr.merge([parameters_dispatch_invest, net_import])
    return p


@pytest.fixture()
def parameter_net_import_single_horizon(parameter_net_import):
    p = parameter_net_import.sel(
        area=["area_1"],
        year_dec=[2040],
        year_inv=[2020],
        year_op=[2020],
    )
    return p


def test_net_import(parameter_net_import_single_horizon):
    p = parameter_net_import_single_horizon.sel(
        conversion_tech=["ocgt", "wind_onshore"],
        hour=[3, 4, 5],
        resource=["electricity", "methane"],
    )
    # Values here corresponds built for a 3 hours operation year duration
    p.operation_year_duration[:] = p.time_step_duration.sum().values
    model = build_model(p)
    model.solve(solver_name="highs")
    s = model.solution.dropna(dim="year_dec", how="all").squeeze()

    assert_equal(s.planning_conversion_power_capacity.to_numpy(), np.array([10, 25]))
    assert_equal(
        s.operation_conversion_power.to_numpy(),
        np.array([[10.0, 5.0, 0.0], [0.0, 5.0, 10.0]]),
    )
    assert_equal(
        s.operation_net_import_import.sel(resource="methane").to_numpy(), np.array([15, 7.5, 0])
    )

    assert_equal(
        s.operation_load_shedding.to_numpy(), np.array([[np.nan, 0], [np.nan, 0], [np.nan, 0]])
    )
    assert_equal(s.operation_spillage.to_numpy(), np.array([[0, 0], [0, 0], [0, 0]]))

    assert model.objective.value == 1120.0
