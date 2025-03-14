# Bootcamp
pip install opencv-python
pip install opencv-contrib-python
pip install opencv-python-headless

가상 환경에서 PyQt5
sudo apt install python3-pyqt5
python3 -m venv --system-site-packages env

pip install ultralytics[export]

sudo apt install -y cmake g++ wget unzip
git clone --depth=1 https://github.com/Tencent/ncnn.git
cd ncnn
mkdir build && cd build
cmake -DNCNN_VULKAN=OFF ..

sudo apt install -y protobuf-compiler libprotobuf-dev
sudo apt install -y libopencv-dev

make -j$(nproc)
sudo make install

sudo apt install fonts-nanum fonts-unfonts-core
sudo apt install fonts-noto-color-emoji