import pandas as pd

from cedarkit.maps.chart import Panel

from cedar_graph.data import DataLoader
from cedar_graph.plots.cn.rain_wind_10m.default import PlotData, PlotMetadata, plot, load_data

from cemc_plots_kit.source import ExprLocalDataSource
from cemc_plots_kit.config import PlotConfig, TimeConfig, ExprConfig, JobConfig
from cemc_plots_kit.logger import get_logger


# set_default_map_loader_package("cedarkit.maps.map.cemc")

PLOT_NAME = "rain_3h_wind_10m"
RAIN_FORECAST_TIME_INTERVAL = pd.Timedelta(hours=3)

plot_logger = get_logger(PLOT_NAME)


def run_plot(job_config: JobConfig) -> Panel:
    expr_config = job_config.expr_config
    time_config = job_config.time_config
    plot_config = job_config.plot_config

    system_name = expr_config.system_name
    start_time = time_config.start_time
    forecast_time = time_config.forecast_time

    metadata = PlotMetadata(
        start_time=start_time,
        forecast_time=forecast_time,
        system_name=system_name,
        area_range=expr_config.area,
        interval=RAIN_FORECAST_TIME_INTERVAL,
    )

    plot_logger.info("loading data...")
    plot_data = load(
        expr_config=expr_config,
        time_config=time_config,
    )
    plot_logger.info("loading data...done")

    # field -> plot
    plot_logger.info("plotting...")
    panel = plot(
        plot_data=plot_data,
        plot_metadata=metadata,
    )
    plot_logger.info("plotting...done")

    del plot_data

    # plot -> output
    return panel


def check_available(time_config: TimeConfig, plot_config: PlotConfig) -> bool:
    return time_config.forecast_time >= pd.Timedelta(hours=3)


def load(expr_config: ExprConfig, time_config: TimeConfig) -> PlotData:
    # system -> data file
    start_time = time_config.start_time
    forecast_time = time_config.forecast_time

    data_source = ExprLocalDataSource(expr_config=expr_config)
    data_loader = DataLoader(data_source=data_source)

    plot_data = load_data(
        data_loader=data_loader,
        start_time=start_time,
        forecast_time=forecast_time,
        interval=RAIN_FORECAST_TIME_INTERVAL,
    )
    return plot_data
