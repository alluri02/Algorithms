

class TwoSum2 {
    public int[] twoSum(int[] numbers, int target) {
        int i =0, j = numbers.length-1;
        int sum;
        while(i < j){
            sum = numbers[i] + numbers[j];
            if(sum > target) {
                j--;
            } else if(sum < target) {
                i++;
            } else {
                return new int[]{i+1,j+1};
            }
        }
        return new int[2];
    }
}
