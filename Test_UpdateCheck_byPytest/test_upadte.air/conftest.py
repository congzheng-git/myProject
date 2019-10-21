import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--apkName", action="store", default="1apk"
    )

@pytest.fixture
def apkName(request):
    return request.config.getoption("--apkName")

def pytest_runtest_makereport(item, call): 
    if "incremental" in item.keywords: 
     if call.excinfo is not None: 
      parent = item.parent 
      parent._previousfailed = item 

def pytest_runtest_setup(item): 
    previousfailed = getattr(item.parent, "_previousfailed", None) 
    if previousfailed is not None: 
     pytest.xfail("previous test failed (%s)" %previousfailed.name)

def pytest_configure(config):
    config._metadata["项目名称"] = "游戏内更新提醒下载测试"
    # 删除Java_Home
    config._metadata.pop("JAVA_HOME")

# @pytest.mark.optionalhook
# def pytest_html_results_summary(prefix):
#     # prefix.extend([html.p("所属部门: xx测试中心")])
#     prefix.extend([html.p("测试人员: 丛政")])

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.pop(-1)  # 删除link列

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.pop(-1)  # 删除link列