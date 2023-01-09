import { FormEvent, useRef } from 'react';
import { Spinner } from 'react-bootstrap';
import { useAppDispatch, useAppSelector } from '../../hooks';
import { loginAction, logoutAction } from '../../redux/auth-actions/auth-actions';
import { getAuthorizationStatus, getIsLoading, getUserEmail, getIsOpen } from '../../redux/auth-actions/selectors';
import actions from '../../redux/auth-actions/auth-proccess';
import { UserStatus } from '../../const';
import { ReactComponent as AccountIcon } from '../../assets/icons/account.svg';
import { ReactComponent as LoginIcon } from '../../assets/icons/login.svg';
import { ReactComponent as LogoutIcon } from '../../assets/icons/logout.svg';

export const Login = (): JSX.Element => {
  const dispatch = useAppDispatch();

  const emailRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const changeIsOpen = actions.changeIsOpen;

  const authorizationStatus = useAppSelector(getAuthorizationStatus);
  const userEmail = useAppSelector(getUserEmail);
  const isLoading = useAppSelector(getIsLoading);
  const isOpen = useAppSelector(getIsOpen);

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
  };

  const LoginForm = () => (
    <form className={`login__form ${isOpen && 'opened'}`} action="/" onSubmit={onFormSubmit}>
      <input type="text" name='email' ref={emailRef} placeholder='Логин' required />
      <input type="password" name='password' ref={passwordRef} placeholder='Пароль' required />
      <button type='submit' className='login__form__button'>
        <LoginIcon />
        {
          isLoading
          ? <Spinner animation='border' size='sm' />
          : 'Войти'
        }
      </button>
    </form>
  );

  const LogoutForm = () => (
    <form className={`login__form ${isOpen && 'opened'}`} action="/" onSubmit={onFormSubmit}>
      <input type="text" name='userEmail' value={userEmail} disabled />
      <button type='submit' className='login__form__button'>
        <LogoutIcon />
        {
          isLoading
          ? <Spinner animation='border' size='sm' />
          : 'Выйти'
        }
      </button>
    </form>
  );

  return (
    <div className='login'>
      <div className={`account_icon ${isOpen && 'opened'}`} onClick={() => dispatch(changeIsOpen(!isOpen))}>
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
