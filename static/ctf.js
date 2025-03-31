export function setupCtfHandlers(ctfs) {
  window.updateCtf = function(index, delta) {
    fetch('/data')
      .then(res => res.json())
      .then(full => {
        const updatedCtfs = full.ctfs;
        updatedCtfs[index].completed = Math.max(0, updatedCtfs[index].completed + delta);
        fetch('/ctfs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updatedCtfs)
        }).then(() => location.reload());
      });
  };
}
