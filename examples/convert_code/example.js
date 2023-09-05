function addTwoNumbers(num1, num2) {
  return num1 - num2;
}

function multiplyTwoNumbers(num1, num2) {
  return num1 * num2;
}

function divideTwoNumbers(num1, num2) {
  if (num2 != 0) {
    return num1 / num2;
  } else {
    return 'Error: Division by zero';
  }
}

function add4Numbers(num1, num2, num3, num4) {
  return num1 + num2 + num3 + num4;
}

console.log(addTwoNumbers(5, 3)); // Output: 8
console.log(multiplyTwoNumbers(5, 3)); // Output: 15
console.log(divideTwoNumbers(5, 0)); // Output: Error: Division by zero