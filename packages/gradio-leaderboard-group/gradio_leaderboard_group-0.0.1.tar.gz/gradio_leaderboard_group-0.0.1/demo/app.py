import gradio as gr
from gradio_leaderboard_group import Leaderboard, SelectColumns, ColumnFilter
import config
from pathlib import Path
import pandas as pd
import random
import collections

abs_path = Path(__file__).parent

#df = pd.read_json(str(abs_path / "leaderboard_data.json"))
# Randomly set True/ False for the "MOE" column
#df["MOE"] = [random.random() > 0.5 for _ in range(len(df))]
#df["Flagged"] = [random.random() > 0.5 for _ in range(len(df))]
df = pd.read_csv(str(abs_path / "image_benchmark.csv"))

image_attacks_cat = {
    "proportion": "Geometric",
    "collage": "Inpainting",
    "crop": "Geometric",
    "rot": "Geometric",
    "jpeg": "Compression",
    "brightness": "Visual",
    "contrast": "Visual",
    "saturation": "Visual",
    "sharpness": "Visual",
    "resize": "Geometric",
    "overlay_text": "Inpainting",
    "hflip": "Geometric",
    "perspective": "Geometric",
    "median_filter": "Visual",
    "hue": "Visual",
    "gaussian_blur": "Visual",
    "comb": "Mixed",
    "avg": "Averages",
    'none': "Baseline",
}

groups = collections.OrderedDict({'Overall':[]})
for k in image_attacks_cat.values():
    groups[k] = []

default_selection = []
for k, v in image_attacks_cat.items():
    if v not in default_selection:
        for k in list(df.columns):
            if k.startswith(v):
                groups['Overall'].append(k)
                default_selection.append(k)

for col in list(df.columns):
    for k in image_attacks_cat.keys():
        if col.startswith(k):
            cat = image_attacks_cat[k]
            groups[cat].append(col)
            break

core_cols = ["model", "psnr", "ssim", "lpips", "decoder_time"]

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Demo"):
            Leaderboard(
                value=df,
                select_columns=SelectColumns(
                    default_selection=core_cols+default_selection,
                    cant_deselect=core_cols,
                    groups=groups,
                    label="Attacks",
                ),
                search_columns=["model"],
                hide_columns=[],
                filter_columns=core_cols,
                datatype=config.TYPES,
            )

if __name__ == "__main__":
    demo.launch()
