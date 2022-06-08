#!/bin/bash
echo "Проверяем лицензию"
/opt/itcs/bin/license status --product=csp_linux

echo "---"
read -p "В выводе должен присутствовать статус State: Valid. Если не Valid укажите y?(y/n)" check_lisence
if [[ "y" == $check_lisence ]]; then
	/opt/itcs/bin/pki-client-license --csp /opt/itcs/share/pki-client/license/1.itcslic
	echo "Команда завершена, необходима перезагрузка"
else
    echo "Вероятно, Вам следует переустановить Vipnet"
fi


