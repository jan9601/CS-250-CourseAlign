function Input({placeholder}) {
  return (
    <input
      placeholder={`${placeholder}`}
      className="h-9 p-2 rounded-lg bg-surface placeholder:text-text-secondary-dark/35 w-full"
    />
  );
}

export default Input;
