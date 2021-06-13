# Scanner İle Taranan Sınav Kağıtlarının OpenCv ile İşlenerek Arşivlenmesi

<link rel="stylesheet" type="text/css" media="all" href="osas\osas\main\static\main\css\md_styles.css" />
<div class="satir">
  <div class="sutun">
    <img src="osas\osas\media\1.png" alt="Sinav_Kagit_Ornegi" style="width:100%">
  </div>
  <div class="sutun">
    <img src="osas\osas\media\Segmentasyon_ goruntusu.png" alt="Kimlik_Numarası_Alinmasi" style="width:80%">
      <div class="satir">
        <img src="osas\osas\media\Qr_Kodun_Alinmasi.png"alt="Qr_kodu_Alinmasi" style="width:80%">
      </div>
      <div class="satir">
        <img src="osas\osas\media\Sistem_Veri_Tabani.png" alt="Sistemin_Veri_Tabani" style="width:80%">
      </div>
  </div>
</div>


> The way algorithm works. Showen in the upper pictures

---


## Description

After reading the exam image it gets splitted into two rectangles from top to bottom then the program starts processing the QR code on the left hand side. For QR code processing Pyzbar library is used. https://github.com/prash29/Barcode-Reader/blob/master/barcode.py the code in the link above is used to extract information stored inside our QR code.

Then the right hand side of the image gets processed. First the box that contains the optic form is recognized using Contours. To find the optic form the code in the link under is used. https://answers.opencv.org/question/230784/finding-rectangle-contours-in-an-image/

After that the optic form gets processed.

### 🛠 &nbsp; Technologies

- 💻 &nbsp;
  ![Python](https://img.shields.io/badge/-Python-333333?style=flat&logo=python)
- 📚 &nbsp;
  ![OpenCv](https://img.shields.io/badge/-OpenCv-333333?style=flat&logo=openCv)
- 🚢 &nbsp;
  ![Docker](https://img.shields.io/badge/-Docker-333333?style=flat&logo=docker)
- 🌐 &nbsp;
  ![HTML5](https://img.shields.io/badge/-HTML5-333333?style=flat&logo=HTML5)
  ![CSS](https://img.shields.io/badge/-CSS-333333?style=flat&logo=CSS3&logoColor=1572B6)
  ![JavaScript](https://img.shields.io/badge/-JavaScript-333333?style=flat&logo=javascript)
  ![Bootstrap](https://img.shields.io/badge/-Bootstrap-333333?style=flat&logo=bootstrap&logoColor=563D7C)
  ![Django](https://img.shields.io/badge/-Django-333333?style=flat&logo=django)
- 🛢 &nbsp;
  ![SQLite](https://img.shields.io/badge/-SQLite-333333?style=flat&logo=sqlite)
- ⚙️ &nbsp;
  ![Git](https://img.shields.io/badge/-Git-333333?style=flat&logo=git)
  ![GitHub](https://img.shields.io/badge/-GitHub-333333?style=flat&logo=github)
  ![Markdown](https://img.shields.io/badge/-Markdown-333333?style=flat&logo=markdown)
- 🔧 &nbsp;
  ![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-333333?style=flat&logo=visual-studio-code&logoColor=007ACC)
  ![Jupyter](https://img.shields.io/badge/-Jupyter-333333?style=flat&logo=jupyter)
  
---

## How To Use

#### Installation

>git clone https://github.com/457341/Bitirme-Projesi.git

#### Go the file path

>cd Bitirme-projesi/osas/osas

#### API Reference

```html
    docker-compose up
```

---

## References
- https://github.com/murtazahassan/Optical-Mark-Recognition-OPENCV
- https://www.udemy.com/course/python-for-computer-vision-with-opencv-and-deep-learning/learn/lecture/12257866?start=0#overview
- https://opencv.org/
- https://github.com/prash29/Barcode-Reader/blob/master/barcode.py
- https://answers.opencv.org/question/230784/finding-rectangle-contours-in-an-image/
- https://www.youtube.com/watch?v=oXlwWbU8l2o&t=5438s&ab_channel=freeCodeCamp.orgfreeCodeCamp.org
- https://www.youtube.com/watch?v=WQeoO7MI0Bs&t=4544s&ab_channel=Murtaza%27sWorkshop-RoboticsandAIMurtaza%27sWorkshop-RoboticsandAIDo%C4%9Fruland%C4%B1
- https://www.youtube.com/playlist?list=PLS1QulWo1RIa7D1O6skqDQ-JZ1GGHKK-K

