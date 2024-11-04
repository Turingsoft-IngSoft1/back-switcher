from utils.profiles import ProfilesManager

def test_profile_id():
    partial_profiles = ProfilesManager()
    prof_id = partial_profiles.get_new_profile()
    assert partial_profiles.get_games(prof_id) == []

def test_add_game():
    partial_profiles = ProfilesManager()
    prof_id = partial_profiles.get_new_profile()
    partial_profiles.add_game(prof_id,1,1)
    assert partial_profiles.get_games(prof_id) == [(1,1)]
    partial_profiles.add_game(prof_id,2,2)
    assert partial_profiles.get_games(prof_id) == [(1,1),(2,2)]

def test_remove_game():
    partial_profiles = ProfilesManager()
    prof_id = partial_profiles.get_new_profile()
    partial_profiles.add_game(prof_id,1,1)
    partial_profiles.add_game(prof_id,2,2)
    partial_profiles.remove_game(prof_id,1,1)
    assert partial_profiles.get_games(prof_id) == [(2,2)]

def test_creates_multiple_profiles():
    partial_profiles = ProfilesManager()
    index_list: list[str] = []
    for _ in range(1000):
        index_list.append(partial_profiles.get_new_profile())
    for i in range(1000):
        assert partial_profiles.get_games(index_list[i]) == []
    assert len(index_list) == 1000