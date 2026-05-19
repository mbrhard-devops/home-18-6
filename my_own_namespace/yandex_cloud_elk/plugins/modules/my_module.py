#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_module
short_description: Creates a text file with specified content on the target host.
version_added: "1.0.0"
description:
    - This module ensures that a text file exists at a specific path with specific content.
options:
    path:
        description:
            - Absolute path to the file to create or update.
        required: true
        type: str
    content:
        description:
            - Content to write into the file.
        required: true
        type: str
author:
    - Your Name (@mbrhard)
'''

EXAMPLES = r'''
- name: Create or update a test file
  my_own_namespace.yandex_cloud_elk.my_module:
    path: /tmp/ansible_test_file.txt
    content: "Hello module!"
'''

RETURN = r'''
path:
    description: The path of the processed file.
    type: str
    returned: always
    sample: '/tmp/ansible_test_file.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'Hello module!'
'''

from ansible.module_utils.basic import AnsibleModule
import os


def main():
    # Определяем входные параметры
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # Инициализируем AnsibleModule
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    file_path = module.params['path']
    desired_content = module.params['content']

    result = dict(
        changed=False,
        path=file_path,
        content=desired_content
    )

    # Проверяем текущее состояние файла
    file_exists = os.path.exists(file_path)
    current_content = ""
    if file_exists:
        with open(file_path, 'r') as f:
            current_content = f.read()

    # Определяем, нужно ли вносить изменения
    needs_change = (not file_exists) or (current_content != desired_content)

    # Режим проверки (dry-run)
    if module.check_mode:
        result['changed'] = needs_change
        module.exit_json(**result)

    # Реальное выполнение
    if needs_change:
        try:
            with open(file_path, 'w') as f:
                f.write(desired_content)
            result['changed'] = True
        except Exception as e:
            module.fail_json(msg=f"Failed to write file: {e}", **result)
    else:
        result['msg'] = "File already exists with correct content."

    # Возвращаем результат в JSON
    module.exit_json(**result)


if __name__ == '__main__':
    main()