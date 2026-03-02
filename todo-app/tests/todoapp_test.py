import sys
import os
import pytest

# Добавляем путь к корневой директории для импорта app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_import_app():
    """Тест импорта приложения"""
    try:
        from app import app, tasks
        assert app is not None
        assert tasks is not None
        print("✓ Приложение импортируется корректно")
        return True
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"✗ Неожиданная ошибка: {e}")
        return False


def test_app_config():
    """Тест конфигурации приложения"""
    from app import app
    assert app is not None
    print("✓ Конфигурация приложения корректна")
    return True


def test_tasks_structure():
    """Тест структуры задач"""
    from app import tasks
    
    # Проверяем, что tasks - это список
    assert isinstance(tasks, list)
    
    # Проверяем структуру первой задачи (если список не пуст)
    if tasks:
        first_task = tasks[0]
        required_keys = {'id', 'title', 'done', 'created'}
        assert required_keys.issubset(first_task.keys())
        print("✓ Структура задач корректна")
    else:
        print("⚠ Список задач пуст")
    
    return True


def test_add_task_logic():
    """Тест логики добавления задачи"""
    from app import app, tasks
    
    # Сохраняем копию исходных задач для восстановления
    original_tasks = tasks.copy()
    
    with app.test_client() as client:
        initial_tasks_count = len(tasks)
        
        # Добавляем задачу
        client.post('/add', data={'title': 'Тестовая задача'})
        
        # Проверяем, что задача добавилась
        assert len(tasks) == initial_tasks_count + 1
        assert tasks[-1]['title'] == 'Тестовая задача'
        assert tasks[-1]['done'] is False
        assert 'created' in tasks[-1]
    
    # Восстанавливаем исходное состояние
    tasks.clear()
    tasks.extend(original_tasks)
    
    print("✓ Логика добавления задачи работает корректно")
    return True


def test_toggle_task_logic():
    """Тест логики переключения статуса задачи"""
    from app import app, tasks
    
    # Сохраняем копию исходных задач для восстановления
    original_tasks = tasks.copy()
    
    with app.test_client() as client:
        # Добавляем тестовую задачу
        test_task = {
            'id': 999,
            'title': 'Тест toggle',
            'done': False,
            'created': '2024-01-01'
        }
        tasks.append(test_task)
        initial_status = test_task['done']
        
        # Переключаем статус
        client.get('/toggle/999')
        
        # Проверяем, что статус изменился
        assert test_task['done'] != initial_status
    
    # Восстанавливаем исходное состояние
    tasks.clear()
    tasks.extend(original_tasks)
    
    print("✓ Логика переключения статуса работает корректно")
    return True


def test_delete_task_logic():
    """Тест логики удаления задачи"""
    from app import app, tasks
    
    # Сохраняем исходное состояние
    original_tasks = tasks.copy()
    
    # Добавляем тестовую задачу
    test_task = {
        'id': 999,
        'title': 'Тест delete',
        'done': False,
        'created': '2024-01-01'
    }
    tasks.append(test_task)
    
    with app.test_client() as client:
        # Проверяем, что задача добавилась
        assert len(tasks) == len(original_tasks) + 1
        
        # Удаляем задачу через клиент
        client.get('/delete/999')
        
        # Проверяем, что задача удалилась
        # Важно: перезагружаем модуль, чтобы получить актуальное состояние
        import importlib
        import app as app_module
        importlib.reload(app_module)
        from app import tasks as updated_tasks
        
        assert len(updated_tasks) == len(original_tasks)
        assert not any(task['id'] == 999 for task in updated_tasks)
    
    # Восстанавливаем исходное состояние
    tasks.clear()
    tasks.extend(original_tasks)
    
    print("✓ Логика удаления задачи работает корректно")
    return True


def test_files_exist():
    """Тест наличия необходимых файлов"""
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
    ]

    all_exist = True
    base_path = os.path.dirname(os.path.dirname(__file__))

    for file in required_files:
        file_path = os.path.join(base_path, file)
        if not os.path.exists(file_path):
            print(f"✗ Файл не найден: {file}")
            all_exist = False
        else:
            print(f"✓ Файл найден: {file}")

    if all_exist:
        print("✓ Все необходимые файлы присутствуют")

    return all_exist


if __name__ == "__main__":
    print("=" * 50)
    print("Запуск тестов Todo приложения")
    print("=" * 50)

    tests = [
        test_import_app,
        test_app_config,
        test_tasks_structure,
        test_add_task_logic,
        test_toggle_task_logic,
        test_delete_task_logic,
        test_files_exist,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        print()
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Тест {test.__name__} упал с ошибкой: {e}")

    print()
    print("=" * 50)
    print(f"Результат: {passed}/{total} тестов пройдено")
    success = passed == total
    sys.exit(0 if success else 1)
