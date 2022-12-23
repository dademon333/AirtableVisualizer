import { FormEvent, useState, useRef } from 'react';
import { useAppDispatch } from '../../hooks';
import { loginAction, logoutAction } from '../../redux/auth-actions/auth-actions';
import { ReactComponent as AccountIcon } from '../../assets/icons/account.svg';
import { ReactComponent as LoginIcon } from '../../assets/icons/login.svg';
import { ReactComponent as LogoutIcon } from '../../assets/icons/logout.svg';

export const Login = (): JSX.Element => {
  const dispatch = useAppDispatch();

  const [isOpen, setIsOpen] = useState<boolean>(false);

  const emailRef = useRef<HTMLInputElement | null>(null);
  const passwordRef = useRef<HTMLInputElement | null>(null);

  const onFormSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (emailRef.current && passwordRef.current) {
      dispatch(loginAction({
        email: emailRef.current.value,
        password: passwordRef.current.value
      }));
      /* dispatch(logoutAction()); */
    }
  }

  return (
    <div className='login'>
      <div className={`account_icon ${isOpen && 'opened'}`} onClick={() => setIsOpen(!isOpen)}>
        <AccountIcon />
      </div>
      <form className={`login__form ${isOpen && 'opened'}`} action="/" onSubmit={onFormSubmit}>
        <input type="text" name='email' ref={emailRef} placeholder='Логин' required />
        <input type="password" name='password' ref={passwordRef} placeholder='Пароль' required />
        <button type='submit'>
          <LoginIcon />
          Войти
        </button>
      </form>
    </div>
  ); 
};
