from subprocess import check_output, DEVNULL

import re

"""
https://github.com/siavash9000/im2txt_demo for the CNN
"""


def parse(output: str) -> str:
    splitted = output.split("\n")
    target = None
    for line in splitted:
        if "0)" in line and "p=" in line:  # ordered 0), 1), 2)
            target = line
    res = re.search(r'\)(.*)\(', target).group(1)
    return res.strip()


# files should include fileformat or might throw an error
def get_description_for_web_img(url: str) -> str:
    path_to_cnn = "/home/kristian/Documents/im2txt_demo"
    cmd = "docker run -i --rm=true -p 8888:8888 -v {}:/root --name=im2txt_demo im2txt_demo sh process_image.sh {}".format(path_to_cnn, url)
    res = str(check_output(cmd, shell=True, stderr=DEVNULL).decode("utf-8"))
    return parse(res)

print(get_description_for_web_img("https://pbs.twimg.com/media/DPly12JXUAAMEc7.jpg"))
