def zipfile(fpath):
    import gzip
    import shutil
    with open(fpath, 'rb') as f_in:
        with open(fpath+'.gz', 'wb') as f_out:
            with gzip.GzipFile(fpath, 'wb', fileobj=f_out) as f_out:
                shutil.copyfileobj(f_in, f_out)
    return True