from .. import generate
import pytest

class TestProcess:
	@pytest.fixture
	def init_process(self):
		self.process = generate.Process()

	def test__transcribe(self, init_process):
		model = "small"
		path = r"C:\Users\keenb\Downloads\吾輩は猫である。...何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。.wav"
		self.result = self.process.convert(model, path)
		assert self.result is not None

	def test__convert_voice(self, init_process):
		pass

	def test__write(self, init_process):
		pass