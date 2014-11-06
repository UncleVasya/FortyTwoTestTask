SCRIPT_FILE_PATH=${0%/*}
OUTPUT_FILE_NAME=$(date +%y-%m-%d).dat
OUTPUT_FILE=${SCRIPT_FILE_PATH}/${OUTPUT_FILE_NAME}

python manage.py print_models 2> ${OUTPUT_FILE}