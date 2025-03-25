def plotColors(pallete: dict, file_length: int) -> list[str]:
    if file_length in [1, 2]:
        color = pallete[3]
        if file_length == 1:
            color = color[:-2]
            return color
        else:
            color = color[:-1]
            return color
    else:
        color = pallete[file_length]
        return color

def themePicker(theme: str):
    theme_name = 'static/files/bokehThemes/' + theme + '_theme.json'
    return theme_name

palette15 = {
    3: ('#FF8A80', '#FFD180', '#CCFF90'),
    4: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF'),
    5: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB'),
    6: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC'),
    7: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740'),
    8: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40'),
    9: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5'),
    10: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081'),
    11: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59'),
    12: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF'),
    13: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40'),
    14: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40', '#607D8B'),
    15: ('#FF8A80', '#FFD180', '#CCFF90', '#80D8FF', '#FF80AB', '#CFD8DC', '#FFD740', '#FF6E40', '#B0BEC5', '#FF4081', '#B2FF59', '#82B1FF', '#FFAB40', '#607D8B', '#FFD180'),
}

palette22 = {
    2: ('#aec7e8', '#ff7f0e'),
    3: ('#aec7e8', '#ff7f0e', '#ffbb78'),
    4: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'),
    5: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'),
    6: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728'),
    7: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'),
    8: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd'),
    9: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5'),
    10: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b'),
    11: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'),
    12: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'),
    13: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'),
    14: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f'),
    15: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7'),
    16: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22'),
    17: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'),
    18: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf'),
    19: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'),
    20: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363'),
    21: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7'),
    22: ('#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7', '#bcbd22')
}

palette23 = {
    3: ('#1f77b4', '#aec7e8', '#ff7f0e'),
    4: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78'),
    5: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c'),
    6: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a'),
    7: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728'),
    8: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896'),
    9: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd'),
    10: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5'),
    11: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b'),
    12: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94'),
    13: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'),
    14: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'),
    15: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f'),
    16: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7'),
    17: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22'),
    18: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d'),
    19: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf'),
    20: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5'),
    21: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363'),
    22: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7'),
    23: ('#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5', '#636363', '#c7c7c7', '#bcbd22')
}
