<?php

declare(strict_types=1);

namespace App\Controllers;

use App\Core\Auth;
use App\Core\Controller;
use App\Models\User;

final class AuthController extends Controller
{
    public function showLogin(): void
    {
        if (Auth::check()) {
            redirect(Auth::isAdmin() ? '/dashboard' : '/');
        }
        $this->view('auth/login', ['title' => 'Iniciar sesión']);
    }

    public function login(): void
    {
        $this->requirePost();
        $email = trim($_POST['email'] ?? '');
        $password = $_POST['password'] ?? '';

        if ($email === '' || $password === '') {
            flash('error', 'Completa email y contraseña.');
            redirect('/login');
        }

        $user = User::verifyCredentials($email, $password);
        if (!$user) {
            flash('error', 'Credenciales incorrectas.');
            redirect('/login');
        }

        Auth::login($user);
        flash('success', 'Bienvenido, ' . $user['name'] . '.');
        redirect($user['role'] === 'admin' ? '/dashboard' : '/');
    }

    public function showRegister(): void
    {
        if (Auth::check()) {
            redirect('/');
        }
        $this->view('auth/register', ['title' => 'Registro']);
    }

    public function register(): void
    {
        $this->requirePost();
        $name = trim($_POST['name'] ?? '');
        $email = trim($_POST['email'] ?? '');
        $password = $_POST['password'] ?? '';
        $confirm = $_POST['password_confirmation'] ?? '';

        if ($name === '' || $email === '' || $password === '') {
            flash('error', 'Todos los campos son obligatorios.');
            redirect('/register');
        }
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            flash('error', 'Email inválido.');
            redirect('/register');
        }
        if (strlen($password) < 6) {
            flash('error', 'La contraseña debe tener al menos 6 caracteres.');
            redirect('/register');
        }
        if ($password !== $confirm) {
            flash('error', 'Las contraseñas no coinciden.');
            redirect('/register');
        }
        if (User::findByEmail($email)) {
            flash('error', 'El email ya está registrado.');
            redirect('/register');
        }

        if (!User::create($name, $email, $password)) {
            flash('error', 'No se pudo crear la cuenta.');
            redirect('/register');
        }

        flash('success', 'Cuenta creada. Ya puedes iniciar sesión.');
        redirect('/login');
    }

    public function logout(): void
    {
        $this->requirePost();
        Auth::logout();
        redirect('/');
    }
}
