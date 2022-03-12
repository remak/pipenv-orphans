#!/usr/bin/env python

import os
import shutil

# Скрипт для обнаружения pipenv окружений-сирот (окружений, рабочих директорий для которых не существует)


HOME_PATH = os.path.expanduser('~')
VIRTUALENVS_PATH = '.local/share/virtualenvs'
PIPENV_PROJECT_FILE = '.project'

envs_dir = os.path.join(HOME_PATH, VIRTUALENVS_PATH)


def search_orphans(vituralenvs_dir):
    # Поиск окружений сирот среди всех имеющихся окружений
    envs_list = os.listdir(vituralenvs_dir)
    envs_orphans = []
    for env in envs_list:
        env_project_file = os.path.join(HOME_PATH, VIRTUALENVS_PATH, env, PIPENV_PROJECT_FILE)
        with open(env_project_file) as file:
            project_dir = file.read()
            if not os.path.exists(project_dir):
                envs_orphans.append(env)
    return envs_orphans


def delete_orphans(list_orphans):
    if list_orphans:
        # Действия (удаление) с окружениями-сиротами
        print('Обнаружено {count_orphans} окружений-сирот'.format(count_orphans=len(list_orphans)))
        do_delete = input('Хотите удалить их из системы? (y/n) ')
        # TODO показывать объем освобождаемого диского простаранства
        if do_delete == 'y':
            print('Будут удалены следующие окружения-сироты:')
            for orphan in list_orphans:
                print(orphan)
            retult = input('Подтвердите Ваш выбор, наберите delete: ')
            if retult == 'delete':
                for orphan in list_orphans:
                    orphan_dir = os.path.join(envs_dir, orphan)
                    shutil.rmtree(orphan_dir, ignore_errors=False)
            else:
                delete_orphans(list_orphans)
        else:
            return
    else:
        print('Окружений-сирот не обнаружено')


orphans = search_orphans(envs_dir)
delete_orphans(orphans)
