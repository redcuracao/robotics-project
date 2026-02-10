export const degreeToRadians = (arr: number[]) => {
  return arr.map(angle => (angle * (Math.PI / 180)));
}

export const radiansToDegrees =(arr: number[]) => {
  return arr.map(rad => rad * (180 / Math.PI));
}

export function reorderArray(arr: number[]) {
  if (arr.length !== 6) {
    throw new Error("배열의 길이는 6이어야 합니다.");
  }

  return [arr[0], arr[1], arr[4], arr[2], arr[3], arr[5]];
}