declare -A sources
sources["slashdot.txt"]="https://snap.stanford.edu/data/soc-Slashdot0811.txt.gz"
sources["google.txt"]="https://snap.stanford.edu/data/web-Google.txt.gz"
sources["gplus.txt"]="https://snap.stanford.edu/data/gplus_combined.txt.gz"
sources["facebook.txt"]="https://snap.stanford.edu/data/facebook_combined.txt.gz"
sources["roadnet_ca.txt"]="https://snap.stanford.edu/data/roadNet-CA.txt.gz"
sources["twitter.txt"]="https://snap.stanford.edu/data/twitter_combined.txt.gz"


for key in ${!sources[@]}; do
    if [ ! -e "${key}" ]; then
        wget ${sources[${key}]} -O ${key}.gz
        gunzip -c ${key}.gz > ${key}
        rm -f ${key}.gz
    fi
done