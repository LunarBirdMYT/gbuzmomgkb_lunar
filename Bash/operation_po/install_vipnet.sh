#!/bin/bash
echo "Устанавливаю VipNet из /opt/vipnet_pki_15"
cd /opt/vipnet_pki_15
sudo sh /opt/vipnet_pki_15/install.sh

echo "---"
read -p "Нужно копировать файл с лицензией из домашней директории в каталог с VipNet?(y/n)" copy_vipnet
if [[ "y" == $copy_vipnet ]]; then
	sudo cp ~/1.itcslic /opt/itcs/share/pki-client/license/1.itcslic
	echo "Файл с лицензией скопирован в каталог с VipNet"
fi

echo "---"
echo "Теперь необходимо обновить версию випнет из /opt/vipnet_pki_16_update"
read -p "Обновляем версию VipNet?(y/n)" get_update
if [[ "y" == $get_update ]]; then
	cd /opt/vipnet_pki_16_update
	sudo sh /opt/vipnet_pki_16_update/install.sh
fi

echo "---"
echo "Установка завершена. Перезагрузите ПК."
