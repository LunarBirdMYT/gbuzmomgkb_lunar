#!/bin/bash
# Функция для проверки и обновления випнет
function check_dir {
	if [[ -d $1 ]]; then
	echo "Директория $1 существует" 
	else
		echo "Нет директории $1"
		if [ -e /opt/itcs/share/pki-client/license/1.itcslic ]; then
			cp /opt/itcs/share/pki-client/license/1.itcslic ~/1.itcslic
			echo "Файл с лицензией скопирован в домашнюю директорию"
		else
			echo "---Файл с лицензией не найден!"
		fi

		read -p "Обновить конфигурацию данных через sudo salt-call state.apply(y/n)?" start_salt
		if [[ "y" == $start_salt ]]; then
			sudo salt-call state.apply
			echo "Выполняю обновление VipNet"
			cd /opt/vipnet_pki_16_update
			sudo sh /opt/vipnet_pki_16_update/install.sh
		fi
	fi
}

echo "Запускаю apt-get update"
sudo apt-get update
echo "---"
echo "Команда выполнена успешно"


echo "---"
echo "Проверяю наличие директорий с VipNet"
check_dir "/opt/vipnet_pki_15"
check_dir "/opt/vipnet_pki_16"
check_dir "/opt/vipnet_pki_16_update"

# Удаление випнет
read -p "Хотите удалить VipNet?(y/n)" del_vipnet

if [[ "y" == $del_vipnet ]]
then
    echo "Копирую файл с лицензией в домашнюю директорию"
	if [ -e /opt/itcs/share/pki-client/license/1.itcslic ]; then
		cp /opt/itcs/share/pki-client/license/1.itcslic ~/1.itcslic
		echo "Файл с лицензией скопирован в домашнюю директорию"
	else
		echo "---Файл с лицензией не найден!"
	fi
	
    echo "Удаляю VipNet посредством remove itcs-*"
    sudo apt-get remove 'itcs-*'
    echo "Удаление VipNet завершено. Выход без перезагрузки."

    count_files=$(ls -l /opt/itcs/ | grep ".prg\|.CRG" | wc -l)
    if [[ $count_files -ne 0 ]]; then
	    echo "---!!! ВНИМАНИЕ! Не хватает прав на удаление всех файлов. Удаление не завершено!"
    fi
else
    echo "Выход без удаления VipNet"
fi
