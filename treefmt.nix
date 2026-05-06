{ pkgs, ... }:
{
  projectRootFile = "flake.nix";

  programs.rustfmt.enable = true;
  programs.ruff-format.enable = true;
  programs.ruff-check.enable = true;
  programs.nixfmt.enable = true;
  programs.taplo.enable = true;

  settings.global.excludes = [
    ".direnv"
    "result"
    "result-*"
    "target"
    "**/target/**"
    ".venv"
    "**/.venv/**"
    ".git"
  ];
}
