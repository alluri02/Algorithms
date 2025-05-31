import java.util.*;
/*
link: https://leetcode.com/problems/combination-sum-ii/
Problem:
Given a collection of candidate numbers (candidates) and a target number (target), 
find all unique combinations in candidates where the candidate numbers sums to target.
Each number in candidates may only be used once in the combination.
Sample:
Input: candidates = [10,1,2,7,6,1,5], target = 8,
A solution set is:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]
Example 2:

Input: candidates = [2,5,2,1,2], target = 5,
A solution set is:
[
  [1,2,2],
  [5]
]
*/

class CombinationSum2 {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> list = new ArrayList<>();
        backtrack(list, new ArrayList<Integer>(), candidates, 0, target);
        return list;

    }
    
    private void backtrack(List<List<Integer>> list,
                          List<Integer> temp,
                          int[] cand, int start, int target){
        
        if(target < 0 ){
            return;
        }else if(target == 0){
            list.add(new ArrayList<>(temp));
        }else{
            for(int i=start; i<cand.length; i++){
                //skip the elements if both are same
                if(i > start && (cand[i] == cand[i-1]))
                    continue;
                temp.add(cand[i]);
                backtrack(list, temp, cand, i+1, target-cand[i]);
                temp.remove(temp.size()-1);
            }
        }
    }
}
