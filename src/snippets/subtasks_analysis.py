from datetime import datetime, timezone, timedelta
from src.services.data import load_json

subtask_ids_to_check = [
    "b709054a-d995-4ef7-a2e9-84400b0b358c", "01db0980-00fa-4102-9900-0461737c7897",
    "474d930f-7ad9-4000-96b0-0abc7aadd91f", "1b000d86-b478-4dd1-8710-890666ee5f29",
    "e106634e-c1b1-407c-817c-d0eea86fd9d0", "7e004089-5b45-490a-b730-329fd0a5b9ba",
    "f086a69a-073e-4c05-a450-406490bf1963", "9064e750-1981-4f45-a36a-e5150083f0e4",
    "1a070912-878f-40c4-bacb-1b9a01333e3b", "b7503801-3a59-418e-a80d-3dc23452e8b0",
    "c962f2b7-dde8-42d1-9314-6c78b5352a59", "9af6b34f-f53f-475d-8716-a16140c43065",
    "334952e3-c22b-4489-ba47-030b8d43acd5", "808006f4-2970-4208-be49-3b9cd8d4a48e",
    "9a7e0ec2-d45e-4a31-a96a-2a24e4685c42", "6cd0bc46-497b-493f-a0b7-02979bedae40",
    "5334523b-0fbd-4ccb-a0a5-c478b7311002", "6aca9923-3218-4c84-be15-cabac41bcbe0",
    "3d391bb9-8e68-4fb7-86bf-d5e92bc3ac6e", "8b0abcc7-6a4e-4ef6-a90f-0900998dcac9",
    "56cdc001-8fdb-4f60-af2a-e812103f0c0a", "e5ef4136-f92c-41c5-8500-e8015b006afb",
    "b909c63b-007a-4fae-ac00-0cf73f6da529", "b7b5fbd0-f96b-43eb-b3dc-2f3f3d76205d",
    "d5e6f9c6-7990-4bcd-a500-054f812be2a5", "8beffb0f-b6aa-42c0-9b83-a4da7da7027e",
    "22920b3b-4177-49bf-9d06-197f160424d0", "01b4cfc3-d762-40dc-930e-9bd068030228",
    "810bf10c-4ec0-4f61-b46b-81bf4a6c1d73", "0ea45a41-b072-40f1-8c71-9e121ef5c26a",
    "83dc4fbb-b1fe-4ee2-9e2b-ac5aa01c1001", "e1be0470-ac88-4bd9-842f-edb6a5cff038",
    "059a6449-0dd0-4cd2-9905-60fcb700416f", "f61a2580-9fc3-47f0-af54-3c2fff95d9d2",
    "237f4312-fb04-4309-b6c9-3138b424541a", "c9608cf7-800c-4540-9300-9b70a0f06d76",
    "49c103ea-d50d-4087-a71e-9899ff1e0210", "68ead9be-97a9-4354-b490-1b5c5aba5c07",
    "aa6e3d5e-8fa2-4bab-95c6-8d0e59f97098", "f8c696d0-100f-4505-ad70-76c6deaa6ec5",
    "7fafdefe-3908-43cd-8ff8-e358534dd697", "af0069c0-5e87-4091-84d0-47d33a08ceab",
    "5afbb9e4-3930-4003-a401-dfabf188d2c4", "70c78019-b60f-404a-aabc-6a82c067b43a",
    "2906fe3d-0601-40bf-bf0e-56e382083a63", "ff5c3543-d6e1-4fd3-bc56-2a91ae086023",
    "fc066c61-f658-40aa-8550-4ee44327fe2c", "3eb215e4-0b4d-4db0-b5e1-e36e2ebaaad1",
    "043b00da-a546-4b55-b4d7-88169e1e1a06", "06118950-59c2-45d0-a5a2-69700ae0e769",
    "6d62dff7-554c-4b65-890a-e08ca9afb07a", "f7491426-b8c8-4f00-b97b-3efb5c0aa946",
    "b305901b-7e0d-45aa-8d2a-66420a050179", "085f2390-7ccc-4926-8002-7fc82580387f",
    "606c0330-6466-4a01-9e76-a0b43a01df49", "485ddfe1-b4b7-4cd3-b314-0d9cfacb9323",
    "60f1c030-4ad1-42ba-80e4-eb525bcb8702", "ef78a6af-1004-4a06-b007-34a22780191e",
    "2d06ac99-a3d0-454b-95e1-582c6ae9e5ba", "9c3ed6d0-0ed2-4d5f-b8fc-1422f66bf741"
]


def subtasks_analysis():
    subtask_data = load_json('subtask.json')
    results = []

    for subtask_id in subtask_ids_to_check:
        subtask = next((st for st in subtask_data if st['id'] == subtask_id), None)
        if subtask:
            timestamp = subtask.get('timestamp')
            if timestamp:
                if isinstance(timestamp, (int, float)):
                    gmt_plus_3 = timezone(timedelta(hours=3))  # временная зона GMT+3
                    creation_date = datetime.fromtimestamp(timestamp / 1000, tz=gmt_plus_3).date()
                else:
                    creation_date = "Неверный формат даты"

                results.append((subtask_id, creation_date))
            else:
                results.append((subtask_id, "Дата создания не найдена"))
        else:
            results.append((subtask_id, "Не найдено в subtask.json"))

    print("Отчёт по дате создания субтасков:")
    for subtask_id, creation_date in results:
        print(f"id: {subtask_id}, дата создания: {creation_date}")


subtasks_analysis()
