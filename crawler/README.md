# Crawler

- Downloads

    1.PostgreSQL - [here](https://www.postgresql.org/download/) (make sure to add it to your path)

- Packages needed

    1.Scrapy - [here](https://docs.scrapy.org/en/latest/intro/install.html)

After succesfull installation. Move to the `Vison-WoC-Backend` directory.

```bash
    $ cd crawler
```
Create a postgresql database using pgAdmin or command line.

Create a table like this:

This command will set up a new table to save the urls.

```sql
    CREATE TABLE urls(
        urlId text,
        rank integer
    )
```
After the execution of the above command, a table with structure like below will be created.

## urls
|urlId | rank|
|------|-----|
|wikipedia.org|1|
|google.com|2|

Execute the following bash command:

```bash
    $ scrapy crawl visonSpider
```
