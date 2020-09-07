import os
import sys

from pathlib import Path
import pytest

from tala.cli import console_script
from tala.utils.chdir import chdir

from tdm.testing.system_integration_testing import ServingMixin


class TestQuickInteractionTests(ServingMixin):
    @classmethod
    def setup_class(cls):
        ddd_path = Path.cwd() / "tdm" / "ddds"
        sys.path.insert(0, str(ddd_path))

    def setup(self):
        super().setup()
        self._working_dir = os.getcwd()
        os.chdir("tdm/ddds")

    def teardown(self):
        super().teardown()
        os.chdir(self._working_dir)

    def then_result_is_successful(self):
        self._assert_no_failure_or_error_exceptions_raised()

    def _assert_no_failure_or_error_exceptions_raised(self):
        pass

    def when_running_tala_test(self, *args):
        args = [f"http://127.0.0.1:{self._port}/interact"] + list(args)
        print(("Running interaction test: 'tala test %s'" % " ".join(args)))
        console_script.main(["test"] + args)

    @pytest.mark.usefixtures("built_literals_grammar")
    def test_literals_grammar(self):
        self.given_serving("literals_grammar.json")
        self.when_running_tala_test("literals_grammar/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_rgl_migration_with_rgl")
    @pytest.mark.parametrize(
        "language,ddd", [("chi", "android"), ("chi", "device_failure"), ("eng", "device_notification")]
    )
    def test_rgl_migration_with_rgl(self, language, ddd):
        with chdir("rgl_migration/with_rgl"):
            self.when_running_tala_test(language, "--config", "%s.config.json" % ddd)
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_mockup_travel")
    @pytest.mark.parametrize(
        "backend_config,ddd_config,test_file", [
            ("mockup_travel_chat.json", "device_failure_with_reason.json", "interaction_tests_eng_chat.txt"),
            (
                "mockup_travel_hi_rerank.json", "device_with_uprankable_answer.json",
                "interaction_tests_eng_hi_rerank.txt"
            ),
            (
                "mockup_travel_low_rerank.json", "device_with_uprankable_answer.json",
                "interaction_tests_eng_low_rerank.txt"
            ),
        ]
    )
    def test_mockup_travel_with_specific_backend_and_ddd_configs(self, backend_config, ddd_config, test_file):
        self.given_serving(backend_config, ddd_configs=[f"mockup_travel:test/{ddd_config}"])
        self.when_running_tala_test(f"mockup_travel/test/{test_file}")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_mockup_travel")
    @pytest.mark.parametrize(
        "ddd_config,test_file", [
            ("device_with_answer_to_trust.json", "interaction_tests_eng_trust_answer_from_device.txt"),
            ("device_with_answer_to_check.json", "interaction_tests_eng_check_answer_from_device.txt"),
            ("device_failure_with_reason.json", "interaction_tests_eng_device_failure_with_reason.txt"),
            ("device_failure_without_reason.json", "interaction_tests_eng_device_failure_without_reason.txt"),
            ("device_where_action_returns_none.json", "interaction_tests_eng_device_where_action_returns_none.txt"),
        ]
    )
    def test_mockup_travel_with_specific_ddd_config(self, ddd_config, test_file):
        self.given_serving("mockup_travel.json", ddd_configs=[f"mockup_travel:test/{ddd_config}"])
        self.when_running_tala_test(f"mockup_travel/test/{test_file}")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_mockup_travel")
    @pytest.mark.parametrize("language", ["eng", "sv", "spa", "pes"])
    def test_mockup_travel_with_default_ddd_config(self, language):
        self.given_serving("mockup_travel.json", language=language, should_greet=True)
        self.when_running_tala_test(f"mockup_travel/test/interaction_tests_{language}.txt")
        self.then_result_is_successful()

    def when_running_tests_for_mockup_travel_with_greeting_in(self, language):
        self.when_running_tala_test(language, "--should-greet", "--config", "mockup_travel.json")

    @pytest.mark.usefixtures("built_mockup_travel")
    def test_mockup_travel_with_semantic_input(self):
        self.given_serving("mockup_travel.json")
        self.when_running_tala_test(f"mockup_travel/test/interaction_tests_semantic.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_hello_world")
    @pytest.mark.parametrize(
        "language,ddd_config,test_file", [
            ("eng", "ddd.config.json", "interaction_tests_eng.txt"),
            ("eng", "test/device_ringing.config.json", "interaction_tests_eng_ringing.txt"),
            ("sv", "ddd.config.json", "interaction_tests_sv.txt"),
        ]
    )
    def test_hello_world(self, language, ddd_config, test_file):
        self.given_serving("hello_world.json", language=language, ddd_configs=[f"hello_world:{ddd_config}"])
        self.when_running_tala_test(f"hello_world/test/{test_file}")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_multi_ddd")
    def test_multi_ddd_english(self):
        with chdir("multi_ddd"):
            self.given_serving(language="eng")
            self.when_running_tala_test(
                "music_player/test/interaction_tests_eng.txt", "navigation/test/interaction_tests_eng.txt"
            )
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_send_to_frontend")
    def test_send_to_frontend(self):
        self.given_serving("send_to_frontend.config.json")
        self.when_running_tala_test("send_to_frontend/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_http_service", "running_service")
    def test_http_service(self):
        self.given_serving("http_service.config.json")
        self.when_running_tala_test("http_service/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_incremental_search")
    def test_incremental_search(self):
        self.given_serving("incremental_search.config.json", language="eng")
        self.when_running_tala_test("incremental_search/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_rgl_migration_without_rgl")
    def test_rgl_migration_without_rgl(self):
        with chdir("rgl_migration/without_rgl"):
            self.given_serving()
            self.when_running_tala_test("android/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_rgl_migration_with_rgl")
    @pytest.mark.parametrize(
        "language,ddd", [
            ("eng", "android"),
            ("fre", "android"),
            ("dut", "android"),
            ("chi", "android"),
            ("eng", "device_failure"),
            ("fre", "device_failure"),
            ("dut", "device_failure"),
            ("chi", "device_failure"),
            ("eng", "device_notification"),
        ]
    )  # yapf: disable
    def test_rgl_migration_with_rgl(self, language, ddd):
        with chdir("rgl_migration/with_rgl"):
            self.given_serving(f"{ddd}.config.json", language=language)
            self.when_running_tala_test(f"{ddd}/test/interaction_tests_{language}.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_tide_pooler")
    def test_tide_pooler(self):
        self.given_serving("tidePooler.json", language="eng")
        self.when_running_tala_test("tidePooler/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_downdate_conditions")
    def test_downdate_conditions(self):
        self.given_serving("downdate_conditions.config.json")
        self.when_running_tala_test("downdate_conditions/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_multi_ddd")
    def test_multi_ddd_swedish(self):
        with chdir("multi_ddd"):
            self.given_serving(language="sv")
            self.when_running_tala_test("music_player/test/interaction_tests_sv.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_output_variation")
    def test_output_variation(self):
        self.given_serving("output_variation.config.json", language="eng")
        self.when_running_tala_test("output_variation/test/interaction_tests_eng.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_phone_directory", "running_phone_directory_service")
    def test_phone_directory(self):
        self.given_serving("phone_directory.config.json", language="sv")
        self.when_running_tala_test("phone_directory/test/interaction_tests_sv.txt")
        self.then_result_is_successful()

    @pytest.mark.usefixtures("built_instructional", "running_instructional_service")
    def test_instructional(self):
        self.given_serving("instructional.config.json", language="eng")
        self.when_running_tala_test("instructional/test/interaction_tests_sem.txt")
        self.then_result_is_successful()
