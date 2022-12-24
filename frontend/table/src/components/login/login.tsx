import { FormEvent, useState, useRef } from 'react';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { loginAction, logoutAction } from '../../redux/auth-actions/auth-actions';
import { getAuthorizationStatus, getUserEmail } from '../../redux/auth-actions/selectors';
import { UserStatus } from '../../const';
import { ReactComponent as AccountIcon } from '../../assets/icons/account.svg';
import { ReactComponent as LoginIcon } from '../../assets/icons/login.svg';
import { ReactComponent as LogoutIcon } from '../../assets/icons/logout.svg';

export const Login = (): JSX.Element => {
  const dispatch = useAppDispatch();

  const [isOpen, setIsOpen] = useState<boolean>(false);

  const emailRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const authorizationStatus = useAppSelector(getAuthorizationStatus);
  const userEmail = useAppSelector(getUserEmail);

  const onFormSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (authorizationStatus === UserStatus.Unauthorized) {
      emailRef.current && passwordRef.current && dispatch(loginAction({
        email: emailRef.current.value,
        password: passwordRef.current.value
      }));
    } else {
      dispatch(logoutAction());
    }
  }

  const LoginForm = () => (
    <form className={`login__form ${isOpen && 'opened'}`} action="/" onSubmit={onFormSubmit}>
      <input type="text" name='email' ref={emailRef} placeholder='Логин' required />
      <input type="password" name='password' ref={passwordRef} placeholder='Пароль' required />
      <button type='submit'>
        <LoginIcon />
        Войти
      </button>
    </form>
  );

  const LogoutForm = () => (
    <form className={`login__form ${isOpen && 'opened'}`} action="/" onSubmit={onFormSubmit}>
      <input type="text" name='userEmail' value={userEmail} disabled />
      <button type='submit'>
        <LogoutIcon />
        Выйти
      </button>
    </form>
  );

  return (
    <div className='login'>
      <div className={`account_icon ${isOpen && 'opened'}`} onClick={() => setIsOpen(!isOpen)}>
        <AccountIcon />
      </div>
      {
        authorizationStatus === UserStatus.Unauthorized 
        ? <LoginForm />
        : <LogoutForm />
      }
    </div>
  ); 
};
