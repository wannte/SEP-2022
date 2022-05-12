import styled from 'styled-components';
import { useToasts } from '@hooks/useToast';
import ToastItem from './ToastItem';

const Wrapper = styled.div`
  position: fixed;
  bottom: 50px;
  right: 0px;
  display: flex;
  flex-direction: column;
  align-items: right;
  z-index: 10000;
  gap: 10px;
`;

const Toast = (): JSX.Element => {
  const toasts = useToasts();
  return (
    <Wrapper>
      {toasts.map((toast: Toast) => (
        <ToastItem key={toast.id} message={toast.message} type={toast.type} duration={toast.duration} />
      ))}
    </Wrapper>
  );
};

export default Toast;
