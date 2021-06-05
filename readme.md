

# Scanner İle Taranan Sınav Kağıtlarının OpenCv ile İşlenerek Arşivlenmesi
<div>
    <tr>
        <td>
          <img src="KimlikNo Alinmasi\Photos\qr2-1.png" width="220" title="Sistem Arayüzü">
        </td>
        <td>
          <img src="KimlikNo Alinmasi\Photos\qr2-1.png"width="220" title="Veri Tabanı">
        </td>
    </tr>
</div>

> Sistemin Arayüzü ile Sistemin Veri Taban Sistemi

---

### Table of Contents
You're sections headers will be used to reference location of destination.

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [License](#license)
- [Contributors](#Contributors)

---

## Description

After reading the exam image it gets splitted into two rectangles from top to bottom then the program starts processing the QR code on the left hand side. For QR code processing Pyzbar library is used. https://github.com/prash29/Barcode-Reader/blob/master/barcode.py the code in the link above is used to extract information stored inside our QR code.

Then the right hand side of the image gets processed. First the box that contains the optic form is recognized using Contours. To find the optic form the code in the link under is used. https://answers.opencv.org/question/230784/finding-rectangle-contours-in-an-image/

After that the optic form gets processed.

#### Technologies

<h3> 🛠 &nbsp;Tech Stack</h3>

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

[Back To The Top](#read-me-template)

---

## How To Use

#### Installation

>git clone https://github.com/457341/Bitirme-Projesi.git

#### API Reference

```html
    docker-compose up
```
[Back To The Top](#read-me-template)

---

## References
- https://github.com/murtazahassan/Optical-Mark-Recognition-OPENCV
- https://www.udemy.com/course/python-for-computer-vision-with-opencv-and-deep-learning/learn/lecture/12257866?start=0#overview
- https://opencv.org/
- https://github.com/prash29/Barcode-Reader/blob/master/barcode.py
- https://answers.opencv.org/question/230784/finding-rectangle-contours-in-an-image/
[Back To The Top](#read-me-template)

---

## Contributors
- Manzoor Hussain
- Tarek 
- Ammar Rahmouni
- Zaid Ahmed

