# Fetchrunner - Retrieve runner race results

This tool fetches running race results for a runner by retrieving informations from Kikourou website.

## 🛠️ Installation


### With PyPI


```bash
pip install fetchrunner
```


### With Github


```bash
git clone https://github.com/arnautt/fetchrunner.git
cd fetchrunner/
pip install -e .
```


### With Docker


```bash
docker build . -t fetchrunner-image
docker run fetchrunner-image fetchrunner --name "Arnaud, Trog"
```


## ⚡ Usage

To fetch race results for a runner, simply use:

```
fetchrunner --name "FirstName, Surname" --save path/to/save/folder
```

Remark: Name format is important, don't forget the comma and start with the first name

## 📄 Output


![CLI output](assets/output.png)



## 📋 TODO

- [] Integrate unit testing in CI/CD
- [] Add automatic deploy to Pypi with Github actions
- [] Handle names with special characters