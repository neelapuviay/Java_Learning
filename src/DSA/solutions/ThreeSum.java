package DSA.solutions;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class ThreeSum {
    public List<List<Integer>> threeSum(int[] nums) {

        // [-4,-1,-1,0,1,2]
        Arrays.sort(nums);
        Set<Integer> set;
        Set<List<Integer>> result = new HashSet<>();

        for (int i = 0; i < nums.length - 1; i++) {
            set = new HashSet<Integer>();
            for (int j = i + 1; j < nums.length; j++) {
                // if (nums[j] == nums[i])
                // continue;
                int a = -(nums[i] + nums[j]);
                if (set.contains(a)) {
                    result.add(Arrays.asList(nums[i], a, nums[j]));
                }
                set.add(nums[j]);
            }
        }
        return new ArrayList(result);

    }

    public static void main(String[] args) {
        int[] nums = { -1, 0, 1, 2, -1, -4 };
        ThreeSum threeSum = new ThreeSum();
        System.out.println(threeSum.threeSum(nums));
    }
}
