param(
    [ValidateRange(1, 1000)]
    [int]$Epochs = 100,
    [ValidateRange(1, 4096)]
    [int]$BatchSize = 32,
    [int]$Seed = 2024,
    [switch]$UseAmp
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = "D:\GPT\freqcycle-venv\Scripts\python.exe"

$runArgs = @(
    "-u", "run.py",
    "--is_training", "1",
    "--model_id", "WPuQ_Household",
    "--model", "FreqCycle",
    "--data", "custom",
    "--root_path", "D:\GPT(work)\date",
    "--data_path", "wpuq_household_hourly.csv",
    "--features", "S",
    "--target", "load_kw",
    "--freq", "h",
    "--paper_split",
    "--seq_len", "8",
    "--label_len", "0",
    "--pred_len", "1",
    "--cycle", "24",
    "--model_type", "mlp",
    "--use_revin", "1",
    "--seg_window", "6",
    "--seg_stride", "6",
    "--window_type", "rect",
    "--d_model", "128",
    "--train_epochs", "$Epochs",
    "--batch_size", "$BatchSize",
    "--learning_rate", "0.001",
    "--lradj", "constant",
    "--loss", "mse",
    "--num_workers", "0",
    "--random_seed", "$Seed",
    "--use_gpu", "1",
    "--gpu", "0",
    "--enc_in", "1",
    "--dec_in", "1",
    "--c_out", "1"
)

if ($UseAmp) {
    $runArgs += "--use_amp"
}

Push-Location $projectRoot
try {
    & $python @runArgs
}
finally {
    Pop-Location
}
