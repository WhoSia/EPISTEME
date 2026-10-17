// P75-P5 independent Go exact integer audit (no new humans/model calls).
// Tests source-relative witness motifs and rational-grid decision minima
// by independent scaled-integer arithmetic, not Python Fraction replay.
package main

import("encoding/json";"fmt";"os";"sort")

type Atom struct{
 Subject,Predicate,Object,Role string
 Valid,Record,Polarity int
 Full,Excerpt bool
 ExpireAt int // zero = no expiry
}
func sourceStatus(src []Atom,validAt,recordAt int,subject,predicate,object string)string{
 positive,negative:=false,false
 for _,a:=range src {
  if a.Valid>validAt || a.Record>recordAt || !a.Full || (a.ExpireAt>0&&validAt>=a.ExpireAt) {continue}
  if a.Subject!=subject||a.Predicate!=predicate||a.Object!=object{continue}
  if a.Polarity==1&&a.Role=="direct_claim"{positive=true}
  if a.Polarity==-1&&a.Role=="direct_defeater"{negative=true}
 }
 if positive&&negative{return "SOURCE_RELATIVE_CONFLICT"}
 if positive{return "SOURCE_RELATIVE_SUPPORT"}
 if negative{return "SOURCE_RELATIVE_DEFEAT"}
 return "SOURCE_RELATIVE_UNDETERMINED"
}
func latest(src []Atom,validAt int)bool{
 for _,a:=range src {if a.Valid<=validAt&&a.Excerpt&&a.Polarity==1{return true}}
 return false
}
func assert(b bool,m string){if !b {fmt.Fprintln(os.Stderr,m);os.Exit(1)}}
func same(a,b []string)bool{
 if len(a)!=len(b){return false}
 for i:=range a{if a[i]!=b[i]{return false}}
 return true
}
// 40 = lcm(1,4,5,8). Losses scaled by 1600, no floating point.
func choose(l,u,k,r int,test bool)([]string,map[string]int){
 loss:=map[string]int{"KEEP":u*40,"SWITCH":(40-l+k)*40}
 if test{loss["REVIEW"]=r*40+u*k}
 best:=1000000
 for _,v:=range loss{if v<best{best=v}}
 acts:=[]string{}
 for act,v:=range loss{if v==best{acts=append(acts,act)}}
 sort.Strings(acts)
 return acts,loss
}
func main(){
 old:=Atom{"a","is","b","direct_claim",1,1,1,true,true,2}
 newW:=Atom{"a","is","b","direct_claim",2,3,1,true,false,0}
 assert(!latest([]Atom{newW},3),"excerpt lost")
 assert(sourceStatus([]Atom{old,newW},2,3,"a","is","b")=="SOURCE_RELATIVE_SUPPORT","source kept")
 assert(sourceStatus([]Atom{old},2,3,"a","is","b")=="SOURCE_RELATIVE_UNDETERMINED","old expired must not appear")
 objection:=Atom{"a","is","b","direct_defeater",2,3,-1,true,false,0}
 newA:=Atom{"a","is","b","direct_claim",2,3,1,true,true,0}
 assert(latest([]Atom{newA,objection},3),"naive latest")
 assert(sourceStatus([]Atom{newA,objection},2,3,"a","is","b")=="SOURCE_RELATIVE_CONFLICT","conflict")
 scope:=Atom{"a","is","b2","direct_claim",2,3,1,true,true,0}
 assert(latest([]Atom{scope},3),"naive scope")
 assert(sourceStatus([]Atom{scope},2,3,"a","is","b")=="SOURCE_RELATIVE_UNDETERMINED","exact scope")
 assert(sourceStatus([]Atom{newA},2,2,"a","is","b")=="SOURCE_RELATIVE_UNDETERMINED","hindsight")
 assert(sourceStatus([]Atom{newA},2,3,"a","is","b")=="SOURCE_RELATIVE_SUPPORT","later record")
 intervals:=[][2]int{{0,40},{10,30},{32,40},{0,8},{20,20}}
 kset:=[]int{0,10,30}; rset:=[]int{0,5,20}
 total,hasTest,noTest,changed,ties:=0,0,0,0,0
 for _,p:=range intervals{for _,k:=range kset{for _,r:=range rset{
  for _,exists:=range []bool{false,true}{
   actions,loss:=choose(p[0],p[1],k,r,exists)
   base,_:=choose(p[0],p[1],k,r,false)
   assert(len(actions)>0&&len(loss)>=2,"empty decision")
   if !same(actions,base){changed++}
   if len(actions)>1{ties++}
   if exists{hasTest++}else{noTest++}
   total++
  }
 }}}
 assert(total==90&&hasTest==45&&noTest==45,"invalid grid size")
 no,los0:=choose(0,40,10,5,false);yes,los1:=choose(0,40,10,5,true)
 assert(same(no,[]string{"KEEP"})&&same(yes,[]string{"REVIEW"}),"missing optional perfect source probe")
 assert(los0["KEEP"]==1600&&los1["REVIEW"]==600,"incorrect regret")
 out:=map[string]any{
   "court":"EPISTEME_P75_P5_INDEPENDENT_GO_INTEGER_AUDIT",
   "status":"PASS",
   "counterexamples_verified":4,
   "grid_cases":total,
   "test_available_cases":hasTest,
   "test_unavailable_cases":noTest,
   "decision_changes_with_perfect_test_offer":changed,
   "action_tie_cases":ties,
   "fixed_conditional_perfect_test_regret":"3/8",
   "human_reviewers":0,
   "strong_full_source_rival_suffices":true}
 enc:=json.NewEncoder(os.Stdout);enc.SetIndent("","  ");assert(enc.Encode(out)==nil,"JSON")
}
