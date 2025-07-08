from app import download_files as df


if __name__ == "__main__":

    urls = df.get_urls()

    for url in urls:

        name = url.get("neighbourhood")
        url = url.get("url")

        print("Begin downloading file for neighbourhood:", name)
        df.download_file_from_url(name, url)

    