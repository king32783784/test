#!/bin/bash/ 
make html
sed -i 's/_static/static/g' _build/html/*.html
sed -i 's/_sources/soures/g' _build/html/*.html
mv _build/html/_static _build/html/static
mv _build/html/_sources _build/html/sources

