from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import StepResult as DotNetStepResult  # noqa

from oakemu.machines.zxspectrum.gameresult import GameResult


class StepResult:
    def __init__(self, step_result: DotNetStepResult):
        self.result: GameResult = GameResult(int(step_result.Result))
        self.score_increase = step_result.ScoreIncrease
