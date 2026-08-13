from huggingface_hub import HfApi, create_repo

api = HfApi()
YOUR_USERNAME = "HanaHailemariam"

create_repo(f"{YOUR_USERNAME}/mt5-en-guz", exist_ok=True)
api.upload_folder(
    folder_path="checkpoints/mt5_combined_guz/final",
    repo_id=f"{YOUR_USERNAME}/mt5-en-guz",
)

create_repo(f"{YOUR_USERNAME}/nllb-en-guz", exist_ok=True)
api.upload_folder(
    folder_path="checkpoints/nllb_combined_guz/final",
    repo_id=f"{YOUR_USERNAME}/nllb-en-guz",
)
print("Done.")