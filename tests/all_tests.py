from ..settings import settings

from .data_for_tests import nested_dictionary_data

from ..src.libraries.supporting import get_hash_dump, unpacking_data

user = settings.test_user

# unpacking_data
unp_data = nested_dictionary_data

out_data = unpacking_data(unp_data, [])
print(out_data)


# actual_dump_hash
out_dir = (
    rf"C:\Users\User\PycharmProjects\instaparser\instaparser\storage\downloads_{user}"
)
ad = {"name": "data_(15-49_20-12-2023).json", "date": "15-49_20-12-2023"}
print(get_hash_dump(out_dir, ad))
