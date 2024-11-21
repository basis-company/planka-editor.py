/*
Макрос для внутреннего редактора скриптов YouGile.
Выводит в журнал терминала архивные сущности всего текущего проекта.
*/

var company_data = Current.project;

if (company_data && company_data.box) {
    var entities = company_data.box.entities;
    var entityKeys = Object.keys(entities);

    for (var i = 0; i < entityKeys.length; i++) {
        var id = entityKeys[i];
        var entityObj = Items.get(id);
        if (!entityObj) {
            continue;
        }

        if (typeof entityObj.isArchived === 'function' && entityObj.isArchived()) {
            console.log(id + " Archived");
        }
    }

    console.log('Done!');
} else {
    console.log('Ошибка: company_data или company_data.box не найдены');
}
