from main_test import frame_detection
from make_coordinate import coordinate


cor=coordinate()
coordinate=cor.get_coordinate()
mai=frame_detection()
mai.run(coordinate[0],coordinate[1],coordinate[2])