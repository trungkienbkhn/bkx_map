# Đề tài: Phân tích dữ liệu người dùng twitter

> Đồ án các công nghệ xây dựng hệ thống thông tin, trường đại học Bách Khoa Hà Nội

## Các chức năng chính

1. Phân tích xu hướng người dùng thông qua hashtag
2. Phân tích location người dùng quan tâm tới một keyword
3. Phân tích cảm xúc bài viêt
4. Phân tích trending thông qua keyword

## Requirements

- Postgresql
- Python3
- twint
- pandas
- matplotlib
- geopy
- nltk
- PyQt5
- psycopg2
- pyvi
- scikit-learn
- tensorflow
- Keras

## Installing

> Đối với hệ điều hành Ubuntu

### Git

```bash
git clone https://gitlab.com/is_soict/it4434_20192/3_hieunk.git
```

### Postgresql

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

- Cài đặt mật khẩu
```bash
sudo -u postgres psql
ALTER USER postgres PASSWORD 'newpassword';
```

### Import database
```bash 
cd Connector/function1/CreateTable
python3 table.py
python3 Copy.py
cd ..
cd ..
cd function2/CreateTable
python3 tablecn2.py
python3 copycn2.py
```

### Run
```bash
cd GUI
python3 app.py
```

## Team

- [ Nguyễn Trung Kiên ] : <https://github.com/trungkienbkhn>
- Nguyễn Phú Tài
- Lê Anh Hào
- Nguyễn Minh Sơn
- Nguyễn Thị Hoài Anh

