<?php

Dotenv\Dotenv::createImmutable(__DIR__)->load();

// Create `database` directory if not exists for migrations

if (!is_dir(__DIR__ . '/database/migrations')) {
    mkdir(__DIR__ . '/database/migrations', 0755, true);
}
if (!is_dir(__DIR__ . '/database/seeds')) {
    mkdir(__DIR__ . '/database/seeds', 0755, true);
}

return
[
    'paths' => [
        'migrations' => '%%PHINX_CONFIG_DIR%%/database/migrations',
        'seeds' => '%%PHINX_CONFIG_DIR%%/database/seeds'
    ],
    'environments' => [
        'default_migration_table' => '__PHINXLOG_MIGRATION',
        'default_environment' => 'default',
        'default' => [
            'adapter' => $_ENV['DB_DRIVER'],
            'host' => $_ENV['DB_HOST'],
            'name' => $_ENV['DB_NAME'],
            'user' => $_ENV['DB_USER'],
            'pass' => $_ENV['DB_PASS'],
            'port' => $_ENV['DB_PORT'],
            'charset' => 'utf8',
        ]
    ],
    'version_order' => 'creation'
];
