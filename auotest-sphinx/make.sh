#!/bin/bash/ 
make html
sed -i 's/_static/static/g' stylebuild/html/*.html
sed -i 's/_sources/soures/g' stylebuild/html/*.html
mv stylebuild/html/_static stylebuild/html/static
mv stylebuild/html/_sources stylebuild/html/sources

