document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('page-ready');
  const revealItems = document.querySelectorAll('.reveal');
  revealItems.forEach((item, index) => {
    item.style.setProperty('--reveal-delay', `${index * 100}ms`);
  });

  const chatThread = document.querySelector('.chat-thread');
  if (chatThread) {
    chatThread.scrollTop = chatThread.scrollHeight;
  }
});
