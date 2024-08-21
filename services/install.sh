SRC_DIR="$PWD/services"
DEST_DIR="/etc/systemd/system/"
NAME=${PWD##*/}

SERVICE_NAME="${NAME}.service"
TIMER_NAME="${NAME}.timer"
ENV_NAME="${NAME}.env"

SERVICE_ORG_SRC="${SRC_DIR}/script.service"
TIMER_ORG_SRC="${SRC_DIR}/script.timer"

SERVICE_PRJ_SRC="${SRC_DIR}/${SERVICE_NAME}"
TIMER_PRJ_SRC="${SRC_DIR}/${TIMER_NAME}"
ENV_PRJ_SRC="${SRC_DIR}/${ENV_NAME}"

SERVICE_PRJ_DST="${DEST_DIR}/${SERVICE_NAME}"
TIMER_PRJ_DST="${DEST_DIR}/${TIMER_NAME}"
ENV_PRJ_DST="/etc/systemd/${ENV_NAME}"

touch "$ENV_PRJ_SRC"
echo "VENV_PATH=${PWD}/venv" >> "${ENV_PRJ_SRC}"
echo "PROJECT_DIR=${PWD}" >> "${ENV_PRJ_SRC}"
echo "NAME=${NAME}" >> "${ENV_PRJ_SRC}"

cp -v "${SERVICE_ORG_SRC}" "${SERVICE_PRJ_SRC}"
cp -v "${TIMER_ORG_SRC}" "${TIMER_PRJ_SRC}"

sed -i "s,{{ envfile }},${NAME}.env,g" "${SERVICE_PRJ_SRC}"
sed -i "s,{{ requires }},${NAME}.service,g" "${TIMER_PRJ_SRC}"

sudo mv -v "${ENV_PRJ_SRC}" "${ENV_PRJ_DST}"
sudo mv -v "${SERVICE_PRJ_SRC}" "${SERVICE_PRJ_DST}"
sudo mv -v "${TIMER_PRJ_SRC}" "${TIMER_PRJ_DST}"

sudo systemctl enable "${TIMER_NAME}"
sudo systemctl start "${TIMER_NAME}"