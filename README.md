#SOLS AUTO CONVERTER

Allow converting file from SOLS AUTO version from old style (.dat) to new style (.csv) and from new style to old style.

Clone repository : 
```shell
git clone git@git.d01.local:it/com/expertise/sols_auto_converter.git
```

Build the image
```shell
docker build --tag=converter .
```

Run the container with your files
```shell
docker run -a stdout -a stderr -v C:\path\to\in:/app/in -v C:\path\to\out:/app/out converter:latest new2old --output_dir=/app/out --parse_type=VEN -v /app/in/Sales_*.csv
```
